import './MessageBubble.css';

const MessageBubble = ({ message, isOwn }) => {
  return (
    <div className={`message-bubble ${isOwn ? 'own' : 'other'}`}>
      <div className="message-header">
        <span className="username">{message.username}</span>
        <span className="timestamp">{new Date(message.created_at).toLocaleTimeString()}</span>
      </div>
      <div className="message-content">
        {message.content}
      </div>
      <div className="message-footer">
        {Object.entries(message.reactions || {}).map(([emoji, count]) => (
          <button key={emoji} className="reaction">
            {emoji} {count}
          </button>
        ))}
      </div>
    </div>
  );
};

export default MessageBubble;
