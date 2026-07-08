import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ChatProvider } from "@/lib/ChatContext";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ResearchMind AI",
  description: "ResearchMind AI - RAG Application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-white text-gray-900 antialiased h-screen overflow-hidden`}>
        <ChatProvider>
          {children}
        </ChatProvider>
      </body>
    </html>
  );
}