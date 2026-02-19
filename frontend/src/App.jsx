import { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDownload = async () => {
    if (!selectedDate) {
      setError('Пожалуйста, выберите дату');
      return;
    }
    const formattedDate = format(selectedDate, 'yyyy-MM-dd');
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:8082/stat_for_month`, {
        params: { dt: formattedDate },
        responseType: 'blob', // important for file download
      });
      // Create a download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${formattedDate}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      setError(err.response?.data?.message || err.message || 'Не удалось скачать CSV');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Статистика по месяцам для базы данных бездомных</h1>
        <p>Выберите месяц для CSV отчета</p>
      </header>
      <main className="main">
        <div className="picker-container">
          <label htmlFor="date-picker">Выберите месяц:</label>
          <DatePicker
            id="date-picker"
            selected={selectedDate}
            onChange={(date) => setSelectedDate(date)}
            dateFormat="yyyy-MM-dd"
            className="date-picker"
            showMonthYearPicker
            showFullMonthYearPicker
            locale={ru}
            dateFormatCalendar="LLLL yyyy"
          />
          <button
            onClick={handleDownload}
            disabled={loading}
            className="download-button"
          >
            {loading ? 'Скачивание...' : 'Скачать CSV'}
          </button>
        </div>
        {error && <div className="error">{error}</div>}
        <div className="instructions">
          <p>
            Результирующий файл будет содержать данные с 1 по последнее число выбранного месяца.
          </p>
        </div>
      </main>
      <footer className="footer">
        <p>Простейшее приложение для бездомных</p>
      </footer>
    </div>
  );
}

export default App;
