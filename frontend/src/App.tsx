import './App.css'
import Start from "./components/Start/Start.tsx";
import {isLogged} from "./store/session.ts";
import Books from "./components/Books/Books.tsx";

function App() {
  return (
    <>
      {isLogged() ? <Books /> : <Start />}
    </>
  )
}

export default App
