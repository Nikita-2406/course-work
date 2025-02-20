import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Импортируем useNavigate
import "./authorization.css";

export const Authorization = ({ SetViewPage }) => {
  const [inputInfo, setInputInfo] = useState({
    login: "",
    password: "",
  });
  const [errorMsg, setErrorMsg] = useState('');
  const navigate = useNavigate(); // Создаем экземпляр navigate

  useEffect(() => {
    const storedLogin = localStorage.getItem('userLogin');
    const storedPassword = localStorage.getItem('userPassword');
    console.log(storedLogin, storedPassword)
    if (storedLogin || storedPassword) {
      fetch('http://127.0.0.1:8000/check_session/', {
      method: "POST",
      body: JSON.stringify({login: storedLogin, password: storedPassword}),
      headers: {
        "Content-Type": "application/json",
      }
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data)
      if (data.status_code === 200) {
        console.log("Вы успешно авторизовались", data)
        navigate('/files', { state: data.user[0] }); // Перенаправляем на страницу файлов
      }
    });
    }
  }, [])

  const onChange = (e) => {
    const { name, value } = e.target;
    setInputInfo((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const onSubmit = (e) => {
    e.preventDefault();
    fetch('http://127.0.0.1:8000/login/', {
      method: "POST",
      body: JSON.stringify(inputInfo),
      headers: {
        "Content-Type": "application/json",
      }
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data)
      if (data.status_code === 200) {
        console.log("Вы успешно авторизовались", data)
        navigate('/files', { state: data.user[0] }); // Перенаправляем на страницу файлов
        localStorage.setItem('userLogin', inputInfo.login);
        localStorage.setItem('userPassword', inputInfo.password);
      } else {
        setErrorMsg("Неверный логин или пароль");
      }
    });
  };

  return (
    <div className="container--form">
      <form onSubmit={onSubmit} className="auth--form">
        <h2 className="head--form">Войти</h2>
        <div className="input--block">
          <input type="text" placeholder="Логин" name="login" onChange={onChange} className="input--form"/>
          <input type="password" placeholder="Пароль" name="password" onChange={onChange} className="input--form"/>
          <div>{errorMsg}</div>
        </div>
        <div className="buttons--block">
          <button type="submit" className="button--form submit">Войти</button>
          <button className="button--form" onClick={() => { SetViewPage("Registration") }}>Зарегестрироваться</button>
        </div>
      </form>
    </div>
  );
};
