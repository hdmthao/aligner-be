import { ADD_SINGLE_USER_CORPUS } from "../Action/type";
import { v4 as uuidv4 } from "uuid";
let initialState = {
  data: [],
};

const UserCorpus = (state = initialState, action) => {
  const { type, payload } = action;

  switch (type) {
    case ADD_SINGLE_USER_CORPUS:
      if (payload.length !== 0) {
        payload.map((item) => (item.id = uuidv4()));
        state.data = [...state.data, ...payload];
      }

      return { ...state };
    default:
      return state;
  }
};

export default UserCorpus;
