import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import DownloadButton from '../files/ButtonDownload';
import { BASEUSLAPI } from '../settings';
export const ShareFilePage = () => {
  const { fileLink } = useParams();
  const [fileData, setFileData] = useState('');
  // console.log(fileLink)

  useEffect(() => {
    if (fileLink !== undefined) {
      const url = `${BASEUSLAPI}files/?link=${fileLink}`;
      console.log(url);
      
      fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error('Сеть не отвечает');
          }
          return response.json();
        })
        .then(data => {
          console.log(data);
          setFileData(data);
        })

    }
  }, [fileLink])
  

  return (
    <>
    <div className='container'>
      <h1>С Вами поделились файлом</h1>
      {fileData.file_name}
      <DownloadButton fileId={fileData.id} />
      {/* {fileName ? <p>Имя файла: {fileName}</p> : <p>Загрузка...</p>} */}
    </div></>
  );
};
