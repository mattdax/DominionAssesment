import { io } from 'socket.io-client'
import { SERVER_HOST, SERVER_PORT } from '../config/config'

const url = 'http://' + SERVER_HOST + ':' + SERVER_PORT
// One Socket.IO connection across telemetry and tool events.
export const socket = io(url, { autoConnect: false })
