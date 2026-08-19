"use client";

import React from "react";

export const SvgSprite: React.FC = () => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" style={{ display: "none" }}>
      <defs>
        {/* OpenAI Symbol */}
        <symbol id="icon-openai" viewBox="0 0 24 24" fill="currentColor">
          <path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zm-1.62-9.76a4.47 4.47 0 0 1 2.34-1.974v5.676a.79.79 0 0 0 .392.682l5.843 3.37-2.02 1.168a.071.071 0 0 1-.065 0l-4.839-2.793a4.504 4.504 0 0 1-1.651-6.129zm15.426 3.673l-5.844-3.37 2.02-1.168a.071.071 0 0 1 .065 0l4.839 2.793a4.515 4.515 0 0 1-.687 8.134v-5.676a.79.79 0 0 0-.393-.713zm2.019-3.027l-.14-.085-4.779-2.759a.775.775 0 0 0-.784 0L7.87 9.715V7.383a.075.075 0 0 1 .033-.062l4.84-2.793a4.5 4.5 0 0 1 6.716 4.391zm-9.317 4.095l2.615-1.51 2.615 1.51v3.018l-2.615 1.51-2.615-1.51z"/>
        </symbol>

        {/* Anthropic Symbol */}
        <symbol id="icon-anthropic" viewBox="0 0 24 24" fill="currentColor">
          <path d="M14.52 3H9.48L3 21h4.48l1.3-3.6h6.44l1.3 3.6H21L14.52 3zm-4.12 11.2l2.6-7.2 2.6 7.2h-5.2z"/>
        </symbol>

        {/* Google Gemini Symbol */}
        <symbol id="icon-gemini" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 0C12 6.627 6.627 12 0 12c6.627 0 12 5.373 12 12 0-6.627 5.373-12 12-12-6.627 0-12-5.373-12-12z"/>
        </symbol>

        {/* DeepSeek Symbol */}
        <symbol id="icon-deepseek" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 16.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
        </symbol>

        {/* Qwen Symbol */}
        <symbol id="icon-qwen" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2L2 7l10 5 10-5-10-5zm0 9l-10-5v9l10 5 10-5v-9l-10 5z"/>
        </symbol>

        {/* Kimi / Moonshot Symbol */}
        <symbol id="icon-kimi" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8A8.96 8.96 0 0 0 12 3z"/>
        </symbol>

        {/* Mistral Symbol */}
        <symbol id="icon-mistral" viewBox="0 0 24 24" fill="currentColor">
          <path d="M3 3h4.5v4.5H3V3zm13.5 0H21v4.5h-4.5V3zM7.5 7.5H12V12H7.5V7.5zm4.5 0h4.5V12H12V7.5zM3 12h4.5v4.5H3V12zm13.5 0H21v4.5h-4.5V12zM7.5 16.5H12V21H7.5v-4.5zm4.5 0h4.5V21H12v-4.5z"/>
        </symbol>

        {/* xAI / Grok Symbol */}
        <symbol id="icon-xai" viewBox="0 0 24 24" fill="currentColor">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
        </symbol>

        {/* Groq Symbol */}
        <symbol id="icon-groq" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 14.5h-2v-5h2v5zm0-7h-2V7h2v2.5z"/>
        </symbol>

        {/* Sound Wave Signal Symbol */}
        <symbol id="icon-wave" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <path d="M2 10v4M6 6v12M10 3v18M14 8v8M18 5v14M22 10v4" />
        </symbol>
      </defs>
    </svg>
  );
};
