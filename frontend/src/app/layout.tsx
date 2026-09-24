import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";
import MainLayout from "@/components/mainLayout";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "900"],
  variable: "--font-poppins",
});


export const metadata: Metadata = {
  title: "Financial Intelligence",
  description: "Understand markets. Discover opportunities.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`h-full antialiased`}
    >
      <body className={`${poppins.variable} min-h-full`}>
        <MainLayout>{children}</MainLayout>
      </body>
    </html>
  );
}
