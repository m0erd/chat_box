// import React, { useState } from "react";
// import { useNavigate } from 'react-router-dom';
// import BaseLayout from "./BaseLayout";

// const Login = ({ setUserAuthenticated }) => {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [errorMessage, setErrorMessage] = useState("");

//   const handleSubmit = async (event) => {
//     event.preventDefault();

//     const loginData = { username, password };

//     try {
//       const response = await fetch("http://127.0.0.1:8001/api/login/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(loginData),
//       });

//       const data = await response.json();

//       if (response.ok) {
//         localStorage.setItem("access_token", data.access_token);
//         localStorage.setItem("refresh_token", data.refresh_token);
//         setUserAuthenticated(true);
//         console.log("Login successful");
//       } else {
//         setErrorMessage(data.error || "An error occurred during login.");
//       }
//     } catch (error) {
//       setErrorMessage("Network error or invalid credentials.");
//     }
//   };

//   return (
//     <BaseLayout>
//       <h2>Login</h2>
//       <form onSubmit={handleSubmit}>
//         <div>
//           <label>Username</label>
//           <input
//             type="text"
//             value={username}
//             onChange={(e) => setUsername(e.target.value)}
//             required
//           />
//         </div>
//         <div>
//           <label>Password</label>
//           <input
//             type="password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//             required
//           />
//         </div>
//         <button type="submit">Login</button>
//       </form>
//       {errorMessage && <p className="error">{errorMessage}</p>}
//     </BaseLayout>
//   );
// };

// export default Login;
