const checkAuthentication = async (login, password) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/check_session/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ login, password }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.status; // Возвращаем данные
  } catch (error) {
    console.error('Ошибка при аутентификации:', error);
    throw error; // Пробрасываем ошибку дальше
  }
};

export default checkAuthentication;
