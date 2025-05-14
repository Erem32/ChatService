# ChatService
!-- Chat Project -->
<h1 style="font-size:2em; font-weight:bold;">Chat Project – Operating Systems 2</h1>

<h2 style="font-size:1.5em; font-weight:bold;">Project Description</h2>
<p>This project implements a chat application that allows multiple clients to communicate simultaneously. The system consists of the following modules:</p>
<ul>
  <li><strong>server.py:</strong> Handles incoming connections, message reception, and broadcasting messages to all connected clients.</li>
  <li><strong>client.py:</strong> Connects to the server and manages sending/receiving messages.</li>
  <li><strong>clientGUI.py:</strong> Provides a graphical user interface (using Tkinter) for user login and communication.</li>
  <li><strong>main.py:</strong> The entry point that starts the server.</li>
</ul>
<p>The project is written in Python and uses multi-threading and synchronization mechanisms to ensure correct handling of simultaneous connections.</p>

<h2 style="font-size:1.5em; font-weight:bold;">Execution Instructions</h2>
<p><strong>Server Execution:</strong></p>
<ol>
  <li>Open a terminal and navigate to the project directory.</li>
  <li>Run the server with:
    <pre>
python main.py
    </pre>
    The server listens for connections on port <strong>5050</strong>.
  </li>
</ol>
<p><strong>Client Execution:</strong></p>
<ol>
  <li>Open a new terminal (or use a different machine) and navigate to the project directory.</li>
  <li>Run the client GUI with:
    <pre>
python client.py
    </pre>
  </li>
  <li>Upon launch, a login screen appears. Enter your username to start chatting.</li>
</ol>

<h2 style="font-size:1.5em; font-weight:bold;">Problem Description</h2>
<p>The chat application addresses the classic inter-process communication challenge in a multi-threaded environment. The main issues include:</p>
<ul>
  <li><strong>Synchronizing access to shared resources:</strong> Ensuring data consistency for the list of active clients and the chat history.</li>
  <li><strong>Handling multi-threading:</strong> Each client connection is handled by a separate thread, requiring proper synchronization to prevent concurrent access issues.</li>
  <li><strong>Managing client disconnections:</strong> Ensuring that disconnected clients are removed from the active list to avoid sending messages to inactive connections.</li>
</ul>

<h2 style="font-size:1.5em; font-weight:bold;">Threads and Their Roles</h2>
<ul>
  <li><strong>On the Server:</strong> For each connected client, a dedicated thread (using the <code>receive_message</code> function in <code>server.py</code>) manages communication.</li>
  <li><strong>On the Client:</strong> The function <code>talk_to_server</code> in <code>client.py</code> starts a separate thread to listen for messages from the server, enabling simultaneous message sending and receiving via the GUI.</li>
</ul>

<h2 style="font-size:1.5em; font-weight:bold;">Critical Sections and Their Handling</h2>
<ul>
  <li><strong>Client List (<code>client_sockets</code>):</strong>
    <ul>
      <li><em>Critical Section:</em> Modifying the list of active connections.</li>
      <li><em>Solution:</em> A lock (<code>client_sockets_lock</code>) ensures that only one thread can modify the client list at a time.</li>
    </ul>
  </li>
  <li><strong>Chat History (<code>chat_history</code>):</strong>
    <ul>
      <li><em>Critical Section:</em> Updating and reading the chat history.</li>
      <li><em>Solution:</em> A lock (<code>chat_history_lock</code>) protects the chat history against simultaneous access from multiple threads.</li>
    </ul>
  </li>
</ul>
