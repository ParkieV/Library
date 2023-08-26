import "./App.css";
import Carousel from "./components/UI/carousel/Carousel";
import Navbar from "./components/UI/navbar/Navbar";

function App() {

  return (
    <div className="App">
      <div className="header__background">
        <header className="header__main">
          <a className="company__logo">Library</a>
          <Navbar/>
        </header>
      </div>
      <main className="main__content">
        <div className="new__products">
          <h2 className="news__title">Новинки</h2>
          <Carousel/>
        </div>
        <div className="books__list">
          <h2 className="books__list__title">Список книг</h2>
          <div className="book">
            <img className="book__img" alt="Book" />
            <div className="book__description">
              <h3 className="book__title">Без названия</h3>
              <p className="book__author">Иван Иванов</p>
              <p className="raiting">4.75/5</p>
            </div>
          </div>
          <div className="book">
            <img className="book__img" alt="Book" />
            <div className="book__description">
              <h3 className="book__title">Без названия</h3>
              <p className="book__author">Иван Иванов</p>
              <p className="raiting">4.75/5</p>
            </div>
          </div>
          <div className="book">
            <img className="book__img" alt="Book" />
            <div className="book__description">
              <h3 className="book__title">Без названия</h3>
              <p className="book__author">Иван Иванов</p>
              <p className="raiting">4.75/5</p>
            </div>
          </div>
        </div>
      </main>
      <footer className="footer__main">
        
      </footer>
    </div>
  );
}

export default App;
