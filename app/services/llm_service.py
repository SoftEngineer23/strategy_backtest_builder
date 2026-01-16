"""Service for interacting with Claude API"""

import anthropic
import re
from pathlib import Path
from app.services.rag_service import RAGService

class LLMService:
    def __init__(self, api_key, model='claude-sonnet-4-20250514', chroma_dir=None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self._system_prompt = None
        self.rag_service = RAGService(chroma_dir) if chroma_dir else None

    def _load_system_prompt(self):
        """Load system prompt from file"""
        if self._system_prompt is None:
            prompt_path = Path(__file__).parent.parent / 'prompts' / 'system_prompt.txt'
            self._system_prompt = prompt_path.read_text()
        return self._system_prompt

    def generate_strategy(self, description):
        """
        Generate strategy code from description
        Returns dict with: success, code, error
        """
        try:
            # Retrieve relevant documentation
            context = ""
            if self.rag_service:
                docs = self.rag_service.retrieve(description, top_k=5)
                context = self.rag_service.format_context(docs)

            # Build the augmented prompt
            if context:
                augmented_message = f"""{context}

              ---

              User request: {description}

              Generate the strategy function based on the request. Use the documentation above for correct syntax."""
            else:
                augmented_message = description

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0,
                system=self._load_system_prompt(),
                messages=[{"role": "user", "content": augmented_message}]
            )

            raw_text = response.content[0].text
            code = self._extract_code(raw_text)

            if code is None:
                return {'success': False,
                        'code': None,
                        'error': 'Could not extract function from response'
                }

            validation = self._validate_code(code)
            if not validation['valid']:
                return {
                    'success': False,
                    'code': code,
                    'error': validation['error']
                }

            return {
                'success': True,
                'code': code,
                'error': None
            }

        except anthropic.APIError as e:
            return {
                'success': False,
                'code': None,
                'error': str(e)
            }

    def _extract_code(self, text):
        """Extract python code from LLM response"""
        # try Markdown code block first
        pattern = r'```python\s*(.*?)\s*```'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            for match in matches:
                if 'def strategy' in match:
                    return match.strip()

        # Try raw function
        if text.strip().startswith('def strategy'):
            return text.strip()

        # Try to find function anywhere in text
        pattern = r'(def strategy\s*\(.*?\):.*?)(?=\ndef |\Z)'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return matches[0].strip()

        return None

    def _validate_code(self, code):
        """validate generated code for safety and accuracy"""
        # check function signature
        if 'def strategy(df)' not in code:
            return {'valid': False, 'error': 'Missing def strategy(df) signature'}

        # Check for dangerous patterns
        dangerous = ['import os', 'import subprocess', 'open(', 'exec(', 'eval(']
        for pattern in dangerous:
            if pattern in code:
                return {'valid': False, 'error': f'Dangerous pattern: {pattern}'}

        # Check syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return {'valid': False, 'error': f'Syntax error: {e}'}

        return {'valid': True, 'error': None}