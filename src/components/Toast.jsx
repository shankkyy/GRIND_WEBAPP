import { AnimatePresence, motion } from 'framer-motion';
import { useStore } from '../stores/useStore';
import './Toast.css';

const Toast = () => {
  const { notifications } = useStore();

  return (
    <div className="toast-container">
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -100, opacity: 0 }}
            className={`toast ${notification.type}`}
          >
            {notification.message}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default Toast;
