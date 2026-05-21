import "./globals.css"
import Sidebar from "@/components/Sidebar"
import Topbar from "@/components/Topbar"
import GlobalAlerts from "@/components/GlobalAlerts"

export const metadata = {
  title: "HRMS Dashboard",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen bg-[#0b1120]">
          <Sidebar />
          <GlobalAlerts />

          <div className="flex flex-1 flex-col overflow-hidden">
            <Topbar />

            <main className="flex-1 overflow-y-auto p-6">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}