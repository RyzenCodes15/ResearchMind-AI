import Sidebar from '@/components/Sidebar';
import ChatBox from '@/components/ChatBox';
import CitationPanel from '@/components/CitationPanel';

export default function HomePage() {
  return (
    <main className="flex h-screen w-full bg-white overflow-hidden">
      <Sidebar />
      <ChatBox />
      <CitationPanel />
    </main>
  );
}