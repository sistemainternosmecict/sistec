import { useState, useContext } from 'react'
import { HostProvider } from './HostContext'
import Login from "./components/Login"
import Home from "./components/Home"
import './App.scss';

function App() {
  const [usuario, setUsuario] = useState({})
  const [loggedIn, setLoggedIn] = useState(false)

  return (
    <HostProvider>
        {
        (loggedIn == true) && (usuario.colab_id) && (usuario.colab_ativo)
        ? <Home usuario={usuario} setUsuario={setUsuario} setLoggedIn={setLoggedIn}/> 
        : <Login setUsuario={setUsuario} setLoggedIn={setLoggedIn}/>
        }
    </HostProvider>
  )
}

export default App
