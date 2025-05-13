import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const backendUrl = process.env.REACT_APP_BACKEND_URL;

const CreateChannel = () => {
  const { user } = useAuth();
  const [channelName, setChannelName] = useState('');
  const [channelDescription, setChannelDescription] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleCreate = async (e) => {
    e.preventDefault();

    if (!user || !user.user_id) {
      console.error('No user ID found in AuthContext');
      setError('You must be logged in to create a channel.');
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/api/channels/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          name: channelName,
          description: channelDescription,
          creator: user.user_id,
        }),
      });

      if (!response.ok) throw new Error('Failed to create channel');

      const data = await response.json();
      console.log('Channel created:', data);

      setSuccessMessage('Channel created successfully!');
      setChannelName('');
      setChannelDescription('');
    } catch (err) {
      console.error('Error creating channel:', err);
      setError('Failed to create channel. Please try again.');
    }
  };

  return (
    <div className="container mt-4">
      <h2>Create a New Channel</h2>

      {error && <div className="alert alert-danger">{error}</div>}
      {successMessage && <div className="alert alert-success">{successMessage}</div>}

      <form onSubmit={handleCreate}>
        <div className="mb-3">
          <label htmlFor="channelName" className="form-label">
            Channel Name
          </label>
          <input
            type="text"
            id="channelName"
            className="form-control"
            value={channelName}
            onChange={(e) => setChannelName(e.target.value)}
            placeholder="Enter channel name"
            required
          />
        </div>

        <div className="mb-3">
          <label htmlFor="channelDescription" className="form-label">
            Channel Description
          </label>
          <textarea
            id="channelDescription"
            className="form-control"
            rows="3"
            value={channelDescription}
            onChange={(e) => setChannelDescription(e.target.value)}
            placeholder="Describe your channel"
          />
        </div>

        <button type="submit" className="btn btn-primary">
          Create Channel
        </button>
      </form>
    </div>
  );
};

export default CreateChannel;
