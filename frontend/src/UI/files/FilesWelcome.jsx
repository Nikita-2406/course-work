import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import UploadFiles from './FilesUpload';
import DownloadButton from './ButtonDownload';
import { sortByDate } from '../sortingDate';
import LogoutButton from '../StartPage/logout';
import { BASEURLWEBSITE, BASEUSLAPI } from '../settings';
// import { p } from 'react-router/dist/development/fog-of-war-DLtn2OLr';

// const BASEURLWEBSITE = "http://localhost:5173/"
// const BASEUSRAPI = 'http://127.0.0.1:8000/'

export const FilesWelcome = () => {
  function formatDate(dateString) {
    // Создаем объект Date из строки
    const date = new Date(dateString);

    // Определяем массив с названиями месяцев
    const months = [
      "января", "февраля", "марта", "апреля",
      "мая", "июня", "июля", "августа",
      "сентября", "октября", "ноября", "декабря"
    ];

    // Получаем компоненты даты
    const hours = String(date.getHours()).padStart(2, '0'); // Часы
    const minutes = String(date.getMinutes()).padStart(2, '0'); // Минуты
    const day = String(date.getDate()).padStart(2, '0'); // День
    const month = months[date.getMonth()]; // Месяц
    const year = date.getFullYear(); // Год

    // Форматируем строку
    return `${hours}:${minutes} ${day} ${month} ${year}`;
  }
  const location = useLocation();
  
  const { id, name, admin, login } = location.state || {};

  if (admin) {
    const navigate = useNavigate()
    useEffect(() => {navigate('/admin/', {state: location.state})}, [])
    // navigate('admin/', {state: location.state})
  } else {
    
    const [viewFiles, setViewFiles] = useState([])
    const [lastFileUpload, setLastFileUpload] = useState(new Date())

    useEffect(() => {
      fetch(`get_files_user/${id}/`)
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        return false
      }
    })
    .then(data => {
      if (data) {
        setViewFiles(sortByDate(data))
      }
    })
    }, [])
  
    useEffect(() => {
      fetch(`${BASEUSLAPI}get_files_user/${id}/`)
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        return false
      }
    })
    .then(data => {
      if (data) {
        setViewFiles(sortByDate(data))
      }
    })
    }, [lastFileUpload])
  
  
    const onGetLink = (id) => {
      // console.log(e.target.parent)
      fetch(`${BASEUSLAPI}get_link_for_file/${id}/`)
      .then(
        response => setLastFileUpload(new Date())
      )
    }
  
    const renameButton = (elem) => {
      const newName = prompt("Введите новое имя файла: ")

      try {
        fetch(`${BASEUSLAPI}files/${elem.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                file_name: newName
            })
        })
        .then(resp => {return resp.json()})
        .then(data => {
          console.log(data)
          setLastFileUpload(new Date())
        })

    } catch (error) {
        console.error('Ошибка:', error);
    }
    }

    return (
      <div className='container'>
        <LogoutButton login={login} />
        <h1>Добро пожаловать, {name}!</h1>
        <button className='button--update--files' onClick={() => {setLastFileUpload(new Date())}}>Обновить список файлов</button>
        <UploadFiles userId={id} setLastFileUpload={setLastFileUpload}/>
        <ul>
        {viewFiles.map(elem => {
          const fileLink = elem.file_link ? `${BASEURLWEBSITE}share/${elem.file_link}` : ''
          return <li id={elem.id} key={elem.id}>
            <span>{elem.file_name}</span>
            <button onClick={() => {renameButton(elem)}}>Переименовать</button><br />
            <span>{formatDate(elem.date)}</span><br />
            < DownloadButton fileId={elem.id}/>
            <button onClick={() => onGetLink(elem.id)}>Поделиться файлом</button><br />
            <a href={fileLink}>{fileLink}</a>
          </li>
        })}
        </ul>
      </div>
    );
  }

  
}
