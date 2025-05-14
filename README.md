[Visit the Real-Time Chat Application](https://frontend-production-7a9d.up.railway.app/)


# 🚀 Real-Time Chat Application with Django

This project showcases a **production-ready real-time chat system** built using **Django**, **Django Channels**, and **PostgreSQL**. It emphasizes:

- Modern backend architecture  
- Asynchronous WebSocket communication  
- Robust security practices  

Users can create and join chat channels, exchange messages instantly, and securely authenticate via **JWT tokens**.

---

## 🧠 Core Engineering Highlights

### ⚙️ Scalable Architecture
- Modular Django design with layered services
- Reusable components and clean separation of concerns

### 🔄 Asynchronous Real-Time Messaging
- Full-duplex WebSocket communication via **Django Channels**

### 🔐 JWT-Based Authentication
- Secure login using access and refresh tokens

### 🛡️ Centralized Error Handling
- Consistent, meaningful HTTP responses for all exceptions

### 🧾 Persistent Chat Storage
- **PostgreSQL** database stores message history and metadata

### 📡 WebSocket Security Layer
- Token-based validation for real-time WebSocket connections

### 📊 Comprehensive Logging System
- Log levels and tracebacks for production-grade debugging

---

## 🔧 Tech Stack

- Django  
- Django REST Framework  
- Django Channels  
- PostgreSQL  
- Redis  
- Docker  
- React

---

## 🐳 Deployment

Deployed on **Railway**  
*(Previously on AWS — switched due to cost)*

---

## ⚠️ Note

> Message persistence was **partially disabled** to accommodate **free-tier database limitations** during deployment.
