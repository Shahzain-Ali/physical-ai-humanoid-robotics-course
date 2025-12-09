import Link from '@docusaurus/Link';
import React from 'react';

export default function Home() {
  return (
    <div style={{ 
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '50vh',
      padding: '2rem',
      textAlign: 'center'
    }}>
      <h1 style={{ color: '#2563eb', fontSize: '2rem', marginBottom: '1rem' }}>Welcome to Physical AI Course</h1>
      <p style={{ fontSize: '1.2rem', margin: '1rem 0', color: '#6b7280' }}>
        A comprehensive course on Physical AI and Humanoid Robotics
      </p>
      <Link 
        to="/docs/" 
        style={{
          padding: '0.75rem 1.5rem',
          fontSize: '1rem',
          backgroundColor: '#2563eb',
          color: 'white',
          borderRadius: '0.5rem',
          textDecoration: 'none',
          display: 'inline-block',
          marginTop: '1rem'
        }}
      >
        Start Learning
      </Link>
    </div>
  );
}
