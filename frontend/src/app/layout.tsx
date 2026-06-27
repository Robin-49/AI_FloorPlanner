import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/ThemeProvider";
import { ChatStoreProvider } from "@/store/chatStore";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI FloorPlanner",
  description: "Your personal AI Architect Assistant for creating and validating floor plans.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} antialiased h-screen overflow-hidden`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <ChatStoreProvider>
            {children}
          </ChatStoreProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
