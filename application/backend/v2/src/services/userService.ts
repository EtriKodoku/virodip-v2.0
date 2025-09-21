import { getDb } from "../mongodb/mongoClient";
import { User } from "../types/User";

const getCollection = async () => {
  const db = await getDb();
  return db.collection("users");
};

export const addUser = async (user: User) => {
  const collection = await getCollection();
  return collection.insertOne(user);
};

export const getUserById = async (id: string) => {
  const collection = await getCollection();
  return collection.findOne({ id });
};

export const getAllUsers = async () => {
  const collection = await getCollection();
  return collection
    .find({}, { projection: { id: 1, displayName: 1, role: 1, _id: 0 } })
    .toArray();
};

export const deleteUser = async (id: string) => {
  const collection = await getCollection();
  return collection.deleteOne({ id });
};

export const updateUserRole = async (id: string, role: string) => {
  const collection = await getCollection();
  return collection.updateOne({ id }, { $set: { role } });
};
