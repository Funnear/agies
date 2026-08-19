import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { StoreProvider } from "@/store/StoreProvider";
import { SvgSprite } from "@/components/SvgSprite";
import { SmoothScroll } from "@/components/SmoothScroll";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "AGIES • Spotify AI Studio Suite & Knowledge Network",
  description: "Advanced Audio Intelligence, Mel-Tempogram Diagnostics, and Knowledge Graph Suite",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-[#07070a] text-[#94a3b8] selection:bg-[#1DB954] selection:text-black">
        <SvgSprite />
        <StoreProvider>
          <SmoothScroll>{children}</SmoothScroll>
        </StoreProvider>
      </body>
    </html>
  );
}
