import React, { useEffect, useState } from "react";
import cls from "./Carousel.module.css"
import Card from "../card/Card";
import BookService from "../../../API/backend/bookService";

const Carousel = () => {

	const [books, setBooks] = useState([]);

	useEffect(async (limit=15, page=1) => {
		response = await BookService.getBookPage(limit, page);
	}, [])

	return (
		<div className={cls.carousel}>
			<div className={cls.cardList}>
				<Card/>
				<Card/>
				<Card/>
				<Card/>
				<Card/>
			</div>
		</div>
	);
};

export default Carousel;