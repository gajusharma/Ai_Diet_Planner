import { FormEvent, useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Bot, Send, X } from "lucide-react";

import api, { extractErrorMessage } from "@/utils/api";

import { useAuth } from "@/context/AuthContext";

type Message = {
  id: string;
  role: "user" | "bot";
  text: string;
};

const ChatBotWidget = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: crypto.randomUUID(),
      role: "bot",
      text: "Hi! Ask me anything about your diet plan, calories, or nutrition tips.",
    },
  ]);
  const messagesRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  useEffect(() => {
    if (open) {
      messagesRef.current?.scrollTo({ top: messagesRef.current.scrollHeight, behavior: "smooth" });
    }
  }, [messages, open]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { id: crypto.randomUUID(), role: "user", text: input.trim() };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const { data } = await api.post<{ reply: string }>("/chat", { message: userMessage.text });
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: crypto.randomUUID(),
          role: "bot",
          text: data.reply,
        },
      ]);
    } catch (error: unknown) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: crypto.randomUUID(), role: "bot", text: extractErrorMessage(error) },
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-40">
      <button
    onClick={() => setOpen((prevOpen) => !prevOpen)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-emerald-500 shadow-xl shadow-emerald-200 transition hover:scale-105 hover:bg-emerald-600"
        aria-label="Open chatbot"
      >
        {open ? <X className="h-6 w-6 text-white" /> : <Bot className="h-7 w-7 text-white" />}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", stiffness: 260, damping: 20 }}
            className="absolute bottom-16 right-0 w-80 overflow-hidden rounded-3xl border border-emerald-100 bg-white shadow-2xl"
          >
            <div className="flex items-center gap-3 bg-gradient-to-r from-emerald-500 to-lime-500 px-4 py-3 text-white">
              <Bot className="h-5 w-5" />
              <div>
                <p className="text-sm font-semibold">Smart Diet Assistant</p>
                <p className="text-xs text-emerald-50">Powered by curated nutrition insights</p>
              </div>
            </div>

            <div ref={messagesRef} className="max-h-96 space-y-3 overflow-y-auto px-4 py-4">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm shadow transition ${
                      message.role === "user"
                        ? "bg-emerald-500 text-white"
                        : "bg-emerald-50 text-emerald-900"
                    }`}
                  >
                    {message.text}
                  </div>
                </motion.div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="flex items-center gap-1 rounded-2xl bg-emerald-50 px-4 py-2 text-xs text-emerald-700">
                    <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
                    <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400 delay-200" />
                    <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400 delay-500" />
                  </div>
                </div>
              )}
            </div>

            <form onSubmit={handleSubmit} className="border-t border-emerald-100 bg-emerald-25 px-4 py-3">
              <div className="flex items-center gap-2 rounded-full border border-emerald-100 bg-white px-3 py-1.5">
                <input
                  value={input}
                  onChange={(event) => setInput(event.target.value)}
                  placeholder="Ask about calories, meals..."
                  className="flex-1 border-none bg-transparent text-sm outline-none focus:ring-0"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="rounded-full bg-emerald-500 p-2 text-white transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ChatBotWidget;
