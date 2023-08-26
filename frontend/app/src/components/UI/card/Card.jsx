import React from "react";

import cls from "./Card.module.css";

const Card = () => {
	return (
		<div className={cls.card}>
			<img className={cls.bookImage} alt="Book"/>
			<h3 className={cls.bookTitle}>Без названия</h3>
			<p className={cls.bookAuthor}>Иван Иванов</p>
		</div>
	);
};

export default Card;