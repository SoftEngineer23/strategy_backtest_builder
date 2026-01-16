import { useEffect, useRef } from 'react';
import hljs from 'highlight.js/lib/core';
import python from 'highlight.js/lib/languages/python';
import 'highlight.js/styles/github-dark.css';

hljs.registerLanguage('python', python);

interface Props {
  code: string;
  onRegenerate: () => void;
}

export function CodeDisplay({ code, onRegenerate }: Props) {
  const codeRef = useRef<HTMLElement>(null);

  useEffect(() => {
    if (codeRef.current) {
      hljs.highlightElement(codeRef.current);
    }
  }, [code]);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
  };

  return (
    <div className="code-display">
      <div className="code-header">
        <h3>Generated Strategy</h3>
        <div className="code-actions">
          <button onClick={copyToClipboard}>Copy</button>
          <button onClick={onRegenerate}>Regenerate</button>
        </div>
      </div>

      <pre>
        <code ref={codeRef} className="language-python">
          {code}
        </code>
      </pre>
    </div>
  );
}
