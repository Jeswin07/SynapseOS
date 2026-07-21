import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Props = {
  content: string;
};

export function MarkdownRenderer({
  content,
}: Props) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ children }) => (
          <h1 className="mt-4 mb-3 text-xl font-bold tracking-tight text-foreground">
            {children}
          </h1>
        ),

        h2: ({ children }) => (
          <h2 className="mt-5 mb-2 text-lg font-semibold tracking-tight text-foreground">
            {children}
          </h2>
        ),

        h3: ({ children }) => (
          <h3 className="mt-4 mb-2 text-base font-semibold text-foreground">
            {children}
          </h3>
        ),

        p: ({ children }) => (
          <p className="mb-3 text-sm leading-6 text-foreground">
            {children}
          </p>
        ),

        ul: ({ children }) => (
          <ul className="mb-3 ml-5 list-disc space-y-1 text-sm">
            {children}
          </ul>
        ),

        ol: ({ children }) => (
          <ol className="mb-3 ml-5 list-decimal space-y-1 text-sm">
            {children}
          </ol>
        ),

        li: ({ children }) => (
          <li className="leading-6">
            {children}
          </li>
        ),

        strong: ({ children }) => (
          <strong className="font-bold text-foreground">
            {children}
          </strong>
        ),

        blockquote: ({ children }) => (
          <blockquote className="my-4 border-l-4 border-primary bg-muted/50 px-4 py-2 italic">
            {children}
          </blockquote>
        ),

        code: ({ children }) => (
          <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-[13px]">
            {children}
          </code>
        ),

        pre: ({ children }) => (
          <pre className="my-4 overflow-x-auto rounded-lg border bg-muted p-4">
            {children}
          </pre>
        ),

        table: ({ children }) => (
          <div className="my-4 overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              {children}
            </table>
          </div>
        ),

        th: ({ children }) => (
          <th className="border bg-muted px-3 py-2 text-left font-semibold">
            {children}
          </th>
        ),

        td: ({ children }) => (
          <td className="border px-3 py-2">
            {children}
          </td>
        ),

        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-primary underline underline-offset-2"
          >
            {children}
          </a>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}