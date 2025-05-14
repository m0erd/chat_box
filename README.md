https://frontend-production-7a9d.up.railway.app/

🚀 Real-Time Chat Application with Django
This project showcases a highly engineered real-time chat system built using Django, Django Channels, and PostgreSQL, emphasizing modern backend architecture, asynchronous communication, and robust security practices.

At its core, the application delivers a production-ready WebSocket infrastructure that allows users to create and join custom chat channels, exchange messages instantly, and securely authenticate via a JWT-based token system.

🧠 Core Engineering Highlights
⚙️Scalable Architecture: Modular Django design, layered service structure, and reusable components ensure clean separation of concerns and future-proofing.
🔄Asynchronous Real-Time Messaging: Django Channels enable full-duplex WebSocket communication for high-performance messaging.
🔐JWT-Based Authentication: Secure token-based login with access and refresh tokens.
🛡️Centralized Error Handling: Consistent and meaningful HTTP responses for all exception cases.
🧾Persistent Chat Storage: PostgreSQL database for structured message history and metadata.
📡WebSocket Security Layer: Token-based connection validation for all real-time interactions.
📊Comprehensive Logging System: Includes log levels and error tracing for production debugging.
🐳Deployment Ready: Docker-based local and cloud deployment.
🔧 Tech Stack
Django, RESTful API, PostgreSQL, Channels, Redis, Docker & React

🚀 Deployment
Railway (previously AWS — switched due to cost).

⚠️ Note
Message persistence was partially disabled to accommodate free-tier database limitations during deployment.