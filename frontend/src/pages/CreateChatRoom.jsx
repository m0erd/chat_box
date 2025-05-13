import React, { useState } from "react";

function CreateChatRoom() {
  const [name, setName] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Creating room:", name);
  };

  return (
    <div>
      <h3>Create a Chatroom</h3>
      <form onSubmit={handleSubmit}>
        <input
          className="form-control mb-2"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Room name"
          required
        />
        <button className="btn btn-success">Create</button>
      </form>
    </div>
  );
}

export default CreateChatRoom;
