import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BASEUSLAPI } from '../settings';

const LogoutButton = ({ login }) => {
  const navigate = useNavigate()
    const handleLogout = async () => {
        fetch(`${BASEUSLAPI}logout/`, {
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
