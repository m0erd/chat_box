import { useEffect, useState } from 'react';

function AppInfo() {
  const [html, setHtml] = useState('');

  useEffect(() => {
    fetch('/app_info.html')
      .then((res) => res.text())
      .then((data) => setHtml(data));
  }, []);

  return (
    <div
      dangerouslySetInnerHTML={{ __html: html }}
      style={{ padding: '2rem', backgroundColor: '#fff' }}
    />
  );
}

export default AppInfo;
