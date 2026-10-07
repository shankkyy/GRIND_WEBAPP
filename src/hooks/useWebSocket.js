import { useEffect, useRef, useCallback } from 'react';
import { useStore } from '../stores/useStore';

export const useWebSocket = (roomId, userId) => {
  const websocketRef = useRef(null);
  const { addMessage, addNotification } = useStore();

  useEffect(() => {
    if (!roomId || !userId) return;

    const wsUrl = `${import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000'}/ws/chat/${roomId}/${userId}`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        switch (data.type) {
          case 'message':
            addMessage(data.data);
            break;

          case 'reaction':
            // Update message reactions
            break;

          case 'user_joined':
            addNotification({
              type: 'info',
              message: `User ${data.user_id} joined`,
              duration: 3000,
            });
            break;

          case 'user_left':
            addNotification({
              type: 'info',
              message: `User ${data.user_id} left`,
              duration: 3000,
            });
            break;

          default:
            console.log('Unknown message type:', data.type);
        }
      } catch (error) {
        console.error('Error processing WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      addNotification({
        type: 'error',
        message: 'Connection error',
      });
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    websocketRef.current = ws;

    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, [roomId, userId, addMessage, addNotification]);

  const sendMessage = useCallback((message) => {
    if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
      websocketRef.current.send(JSON.stringify(message));
    }
  }, []);

  return { sendMessage };
};
