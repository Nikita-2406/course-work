import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = ({ login }) => {
  const navigate = useNavigate()
    const handleLogout = async () => {
        fetch('http://127.0.0.1:8000/logout/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({login: login}),
            })
            .then(resp => {
              if (resp.ok) {
                return resp.json();
              } else {
                return "Error";
              }
            })
            .then(data => {
              if (data.status == "deleted") {
                localStorage.clear()
                navigate("/", { replace: true });
              } else {
                alert("Возникла какая то ошибка")
              }
            })
    };

    return (
        <button onClick={handleLogout}>
            Выйти
        </button>
    );
};

export default LogoutButton;
