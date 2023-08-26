import axios from "axios";
import URL from "./../../settings/APISettings";

export default class BookService {
  static async getBookPage(limit = 15, page = 1) {
    const response = await axios.get(URL + "book_table/", {
      params: {
        limit: limit,
        page: page,
      },
    });
    return response;
  }
}
