import MainLayout from "../components/layout/MainLayout";
import Sidebar from "../components/layout/Sidebar";
import RightPanel from "../components/layout/RightPanel";
import ChatWindow from "../components/chat/ChatWindow";

function Home() {
  return (
    <MainLayout
      sidebar={<Sidebar />}
      chat={<ChatWindow />}
      insights={<RightPanel />}
    />
  );
}

export default Home;