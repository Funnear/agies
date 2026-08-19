"use client";

import React from "react";

export type IconName =
  | "openai"
  | "anthropic"
  | "gemini"
  | "deepseek"
  | "qwen"
  | "kimi"
  | "mistral"
  | "xai"
  | "groq"
  | "wave";

interface IconProps extends React.SVGProps<SVGSVGElement> {
  name: IconName;
  className?: string;
  size?: number | string;
}

export const Icon: React.FC<IconProps> = ({
  name,
  className = "w-4 h-4",
  size,
  style,
  ...props
}) => {
  const customStyle: React.CSSProperties = {
    ...style,
    ...(size ? { width: size, height: size } : {}),
  };

  return (
    <svg className={`inline-block shrink-0 ${className}`} style={customStyle} {...props}>
      <use href={`#icon-${name}`} />
    </svg>
  );
};
