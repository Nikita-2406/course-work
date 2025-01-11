import { useState } from 'react'
import './App.css'
import { StartPage } from './UI/StartPage/StartPage'
import { FilesWelcome } from './UI/files/FilesWelcome'
import { Routes, Route, BrowserRouter } from "react-router"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/files" element={<FilesWelcome />} />
      </Routes>
    </BrowserRouter>
      {/* <StartPage /> */}
    </>
  )
}

export default App
