import { useEffect, useRef, useState } from 'react';

export function useWebSocket(url) {
  const [messages, setMessages] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(url);
    ws.current.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };
    return () => ws.current?.close();
  }, [url]);

  const send = (data) => {
    ws.current?.send(JSON.stringify(data));
  };

  return { messages, send };
}
