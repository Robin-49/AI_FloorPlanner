import { Header } from "@/components/Layout/Header";
import { Sidebar } from "@/components/Layout/Sidebar";
import { ChatContainer } from "@/components/Chat/ChatContainer";

export default function Home() {
  return (
    <div className="flex flex-col h-screen">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 flex flex-col relative w-full h-full">
          <ChatContainer />
        </main>
      </div>
    </div>
  );
}
