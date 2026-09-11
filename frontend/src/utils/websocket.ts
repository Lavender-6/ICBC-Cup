type MessageHandler = (data: any) => void

export class WebSocketClient {
  private ws: WebSocket | null = null
  private handlers: Map<string, Set<MessageHandler>> = new Map()
  private reconnectTimer: number | null = null

  connect(url: string = `ws://${window.location.host}/ws`) {
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      if (this.reconnectTimer) {
        clearTimeout(this.reconnectTimer)
        this.reconnectTimer = null
      }
    }

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        const handlers = this.handlers.get(message.type)
        handlers?.forEach((handler) => handler(message.data))
      } catch (e) {
        console.error('WebSocket message parse error:', e)
      }
    }

    this.ws.onclose = () => {
      console.log('WebSocket disconnected, reconnecting in 3s...')
      this.reconnectTimer = window.setTimeout(() => this.connect(url), 3000)
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }

  on(type: string, handler: MessageHandler) {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set())
    }
    this.handlers.get(type)!.add(handler)
  }

  off(type: string, handler: MessageHandler) {
    this.handlers.get(type)?.delete(handler)
  }

  send(type: string, data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, data }))
    }
  }

  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
    }
    this.ws?.close()
    this.ws = null
  }
}

export const wsClient = new WebSocketClient()
