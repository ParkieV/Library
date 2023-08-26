import React from "react";

import cls from "./Navbar.module.css";

const Navbar = () => {
	return (
		<nav className={cls.navbarMain}>
				<a href="#" className={cls.link}>Книги</a>
				<a href="#" className={cls.link}>Пользователи</a>
				<a href="#" className={cls.link}>Запросы</a>
			<div className={cls.searchBar}>
				<form className={cls.searchForm}>
					<input className={cls.input} defaultValue="Поиск книги" />
				</form>
				<button className={cls.searchButton}></button>
			</div>
				<div className={cls.notifications}>
					<div className={cls.notificationButton}></div>
				</div>
				<div className={cls.avatar}>
					<div className={cls.avatarImage}/>
				</div>
		</nav>
	);
};

export default Navbar;