// pages/index.tsx
import React, { useState } from 'react';
import Head from 'next/head';
import { EnhancedChatInterface } from '../components/EnhancedChat';

export default function SDLCAssistant() {
  const [sessionId] = useState(() => `session_${Date.now()}`);

  return (
    <>
      <Head>
        <title>FLUX - Where Agents Meet Agile</title>
        <meta name="description" content="FLUX - Where Agents Meet Agile. AI-powered development platform with specialized agents and GitHub integration" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <EnhancedChatInterface sessionId={sessionId} />
    </>
  );
}