import { useState } from 'react'
import './App.css'
import { StartPage } from './UI/StartPage/StartPage'
import { FilesWelcome } from './UI/files/FilesWelcome'
import { Routes, Route, BrowserRouter } from "react-router-dom"
import { AdminPage } from './UI/admin/AdminPage'
import { ViewFilesUser } from './UI/admin/ViewFilesUser'
import { ShareFilePage } from './UI/ShareFilePage/ShareFilePage'

function App() {

  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/files" element={<FilesWelcome />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/files_user" element={<ViewFilesUser />} />
        <Route path="/share/:fileLink" element={<ShareFilePage />} />
      </Routes>
    </BrowserRouter>
    </>
  )
}

export default App
