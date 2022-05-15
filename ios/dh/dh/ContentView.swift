//
//  ContentView.swift
//  dh
//
//  Created by Žiga Patačko Koderman on 14/05/2022.
//

import SwiftUI
import Starscream

struct ContentView: View {
    var socket: WebSocket

    init() {
        var request = URLRequest(url: URL(string: "http://88.200.88.177:6969")!)
        request.timeoutInterval = 5
        socket = WebSocket(request: request)
        socket.connect()
//        let asdf = "asdf\n".data(using: .utf8)!
//        socket.write(string: "asdf")
//        socket.disconnect()
    }


    func didReceive(event: WebSocketEvent, client: WebSocket) {
        print("received")
    }

    func websocketDidConnect(socket: WebSocketClient) {
        print("websocket is connected")
        socket.write(string: "asdf")
    }

    var body: some View {
        Text("Hello, world!")
                .padding()
        Button(action: {
            socket.write(string: "asdf")
        }) {
            Text("asdf")
        }
//        Button(action: <#T##@escaping () -> Void##@escaping () -> Swift.Void#>, label: <#T##@ViewBuilder () -> Label##@ViewBuilder () -> Label#>)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
