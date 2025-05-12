// import React, { useEffect, useRef, useState } from 'react';

// export default function ChatPanel() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState('');
//   const socketRef = useRef(null);

//   useEffect(() => {
//     const chatChannelName = 'general';
//     socketRef.current = new WebSocket(`ws://${window.location.host}/ws/chat/${chatChannelName}/`);

//     socketRef.current.onmessage = (e) => {
//       const data = JSON.parse(e.data);
//       setMessages((prev) => [...prev, data.message]);
//     };

//     return () => socketRef.current.close();
//   }, []);

//   const sendMessage = () => {
//     if (input.trim() && socketRef.current) {
//       socketRef.current.send(JSON.stringify({ message: input }));
//       setInput('');
//     }
//   };

//   return (
//     <>
//       <h3>Channel Name</h3>
//       <div className="message-list">
//         {messages.map((msg, i) => <div key={i} className="message">{msg}</div>)}
//       </div>
//       <div className="message-input">
//         <input
//           type="text"
//           className="form-control"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
//           placeholder="Type your message..."
//         />
//         <button className="btn btn-primary w-100 mt-2" onClick={sendMessage}>Send</button>
//       </div>
//     </>
//   );
// }
