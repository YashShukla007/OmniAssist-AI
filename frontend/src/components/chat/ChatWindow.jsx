import Navbar from "../layout/Navbar";
import ChatArea from "./ChatArea";
import PromptInput from "./PromptInput";

function ChatWindow() {
  return (
    <div className="flex flex-col h-full">
      <Navbar />

      <ChatArea />

      <PromptInput />
    </div>
  );
}

export default ChatWindow;