import { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useStore } from '../stores/useStore';
import { chatAPI } from '../api/client';
import { useWebSocket } from '../hooks/useWebSocket';
import MessageBubble from './MessageBubble';
import './Chat.css';

const Chat = () => {
  const { user, currentRoom, messages, setMessages, addMessage } = useStore();
  const [inputValue, setInputValue] = useState('');
  const [selectedRoom, setSelectedRoom] = useState('default-room');
  const messagesEndRef = useRef(null);
  
  const { sendMessage } = useWebSocket(selectedRoom, user.id);

  // Fetch messages
  const { data: fetchedMessages = [] } = useQuery({
    queryKey: ['messages', selectedRoom],
    queryFn: () => chatAPI.getMessages(selectedRoom, 50, 0),
    enabled: !!selectedRoom,
    select: (response) => response.data,
  });

  // Send message mutation
  const sendMutation = useMutation({
    mutationFn: (content) => chatAPI.sendMessage(selectedRoom, content),
    onSuccess: (response) => {
      const message = response.data.message;
      addMessage(message);
      setInputValue('');
    },
  });

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Update messages
  useEffect(() => {
    if (fetchedMessages.length > 0) {
      setMessages(fetchedMessages);
    }
  }, [fetchedMessages, setMessages]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !sendMutation.isPending) {
      sendMutation.mutate(inputValue.trim());
    }
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="header-content">
          <h2>Room: {selectedRoom}</h2>
          <span className="room-members">👥 1 member</span>
        </div>
        <button className="header-btn">⚙️</button>
      </div>

      {/* Messages */}
      <div className="messages-list">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message}
            isOwn={message.user_id === user.id}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSendMessage} className="input-area">
        <div className="input-row">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message..."
            maxLength={500}
            disabled={sendMutation.isPending}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || sendMutation.isPending}
            className="send-btn"
          >
            {sendMutation.isPending ? '...' : 'SEND'}
          </button>
        </div>
        {inputValue.length > 400 && (
          <span className="char-count">
            {inputValue.length}/500
          </span>
        )}
      </form>

      {/* Quick Action Buttons */}
      <div className="quick-actions">
        <button className="action-btn" title="Spin Wheel">🎡</button>
        <button className="action-btn" title="Clash Battle">🎮</button>
        <button className="action-btn" title="Emeralds">💰</button>
        <button className="action-btn" title="Streak">🔥</button>
        <button className="action-btn" title="Challenge">⚡</button>
        <button className="action-btn" title="Stats">📊</button>
      </div>
    </div>
  );
};

export default Chat;
