import { useState } from "react"
import "./authorization.css"

export const Authorization = ({SetViewPage}) => {

  const [inputInfo, setInputInfo] = useState({
    login: "",
    password: "",
  })
  const [errorMsg, setErrorMsg] = useState('')

  const onChange = (e) => {
    const { name, value } = e.target
    setInputInfo((prev) => ({
    ...prev, 
    [name]: value
  }))
  }

  const onSubmit = (e) => {
    e.preventDefault()
    // console.log(inputInfo)
    fetch('http://127.0.0.1:8000/check_password/', {
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
    if (data.status_code === 200) {
      SetViewPage("UserFiles")
    } else {
      setErrorMsg("Неверный логин или пароль")
    }
  });
  }  


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
          <button className="button--form" onClick={() => {SetViewPage("Registration")}}>Зарегестрироваться</button>
        </div>
        
        
      </form>
      {/* <button onClick={funk}>123123123</button> */}
    </div>
  )
}