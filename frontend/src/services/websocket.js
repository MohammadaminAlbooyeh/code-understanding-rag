class WebSocketService {
  constructor() {
    this.ws = null;
  }

  connect(url) {
    this.ws = new WebSocket(url);
    this.ws.onopen = () => console.log('WebSocket connected');
    this.ws.onclose = () => console.log('WebSocket disconnected');
  }

  send(data) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  onMessage(callback) {
    if (this.ws) {
      this.ws.onmessage = (event) => callback(JSON.parse(event.data));
    }
  }

  disconnect() {
    this.ws?.close();
  }
}

export default new WebSocketService();
