/*
See LICENSE folder for this sample’s licensing information.

Abstract:
A view that displays scene depth information.
*/

import Foundation
import SwiftUI
import MetalKit
import Metal
import Foundation
import SwiftUI
import Combine
import ARKit
import Network
import Accelerate
import MobileCoreServices
import MetalPerformanceShaders
import Starscream

//- Tag: CoordinatorDepth
final class CoordinatorDepth: MTKCoordinator {
    var socket: WebSocket
    @Binding var confSelection: Int

    init(mtkView: MTKView, depthContent: MetalTextureContent, confSelection: Binding<Int>) {
        self._confSelection = confSelection
        var request = URLRequest(url: URL(string: "http://192.168.46.77:6969")!)
        request.timeoutInterval = 5
        socket = WebSocket(request: request)
        socket.connect()
        super.init(content: depthContent, view: mtkView)
    }

    override func prepareFunctions() {
        guard let metalDevice = view.device else {
            fatalError("Expected a Metal device.")
        }
        do {
            let library = EnvironmentVariables.shared.metalLibrary
            let pipelineDescriptor = MTLRenderPipelineDescriptor()
            pipelineDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
            pipelineDescriptor.vertexFunction = library.makeFunction(name: "planeVertexShader")
            pipelineDescriptor.fragmentFunction = library.makeFunction(name: "planeFragmentShaderDepth")
            pipelineDescriptor.vertexDescriptor = createPlaneMetalVertexDescriptor()
            pipelineState = try metalDevice.makeRenderPipelineState(descriptor: pipelineDescriptor)
        } catch {
            print("Unexpected error: \(error).")
        }
    }

    func swizzleBGRA8toRGBA8(_ bytes: UnsafeMutableRawPointer, width: Int, height: Int) {
        var sourceBuffer = vImage_Buffer(data: bytes,
                height: vImagePixelCount(height),
                width: vImagePixelCount(width),
                rowBytes: width * 4)
        var destBuffer = vImage_Buffer(data: bytes,
                height: vImagePixelCount(height),
                width: vImagePixelCount(width),
                rowBytes: width * 4)
        var swizzleMask: [UInt8] = [ 2, 1, 0, 3 ] // BGRA -> RGBA
        vImagePermuteChannels_ARGB8888(&sourceBuffer, &destBuffer, &swizzleMask, vImage_Flags(kvImageNoFlags))
    }

    var i = 0

    override func draw(in view: MTKView) {
        guard content.texture != nil else {
            print("There's no content to display.")
            return
        }
        guard let commandBuffer = metalCommandQueue.makeCommandBuffer() else { return }
        guard let passDescriptor = view.currentRenderPassDescriptor else { return }
        guard let encoder = commandBuffer.makeRenderCommandEncoder(descriptor: passDescriptor) else { return }
        let vertexData: [Float] = [  -1, -1, 1, 1,
                                     1, -1, 1, 0,
                                     -1, 1, 0, 1,
                                     1, 1, 0, 0]
        encoder.setVertexBytes(vertexData, length: vertexData.count * MemoryLayout<Float>.stride, index: 0)
        encoder.setFragmentTexture(content.texture, index: 0)
        encoder.setRenderPipelineState(pipelineState)
        encoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 4)
        encoder.endEncoding()
        commandBuffer.present(view.currentDrawable!)
        commandBuffer.commit()

        // TLE

        if (i % 6 == 0) {
            let width = view.currentDrawable!.texture.width
            let height = view.currentDrawable!.texture.height
            let pixelByteCount = 4 * MemoryLayout<UInt8>.size
            let imageBytesPerRow = (width) * pixelByteCount
            let imageByteCount = imageBytesPerRow * (height)
            let imageBytes = UnsafeMutableRawPointer.allocate(byteCount: imageByteCount, alignment: pixelByteCount)
            defer {
                imageBytes.deallocate()
            }


            view.currentDrawable?.texture.getBytes(imageBytes,
                    bytesPerRow: imageBytesPerRow,
                    from: MTLRegionMake2D(0, 0, width ?? 0, height ?? 0),
                    mipmapLevel: 0)
            swizzleBGRA8toRGBA8(imageBytes, width: width ?? 0, height: height ?? 0)

            guard let colorSpace = CGColorSpace(name: CGColorSpace.linearSRGB) else {
                return
            }
            let bitmapInfo = CGImageAlphaInfo.premultipliedLast.rawValue
            guard let bitmapContext = CGContext(data: nil,
                    width: width ?? 0,
                    height: height ?? 0,
                    bitsPerComponent: 8,
                    bytesPerRow: imageBytesPerRow,
                    space: colorSpace,
                    bitmapInfo: bitmapInfo)
            else {
                return
            }
            bitmapContext.data?.copyMemory(from: imageBytes, byteCount: imageByteCount)
            let image = bitmapContext.makeImage()!

            let result = UIImage(cgImage: image)
            socket.write(data: result.jpegData(compressionQuality: 0.1) ?? Data())

        }
        i += 1
    }

}

struct MetalTextureViewDepth: UIViewRepresentable {
    var mtkView: MTKView
    var content: MetalTextureContent

    @Binding var confSelection: Int

    func makeCoordinator() -> CoordinatorDepth {
        CoordinatorDepth(mtkView: mtkView, depthContent: content, confSelection: $confSelection)
    }

    func makeUIView(context: UIViewRepresentableContext<MetalTextureViewDepth>) -> MTKView {
        mtkView.delegate = context.coordinator
        mtkView.preferredFramesPerSecond = 60
        mtkView.backgroundColor = context.environment.colorScheme == .dark ? .black : .white
        mtkView.isOpaque = true
        mtkView.framebufferOnly = false
        mtkView.clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 0)
        mtkView.drawableSize = mtkView.frame.size
        mtkView.enableSetNeedsDisplay = false
        mtkView.colorPixelFormat = .bgra8Unorm
        return mtkView
    }

    // `UIViewRepresentable` requires this implementation; however, the sample
    // app doesn't use it. Instead, `MTKView.delegate` handles display updates.
    func updateUIView(_ uiView: MTKView, context: UIViewRepresentableContext<MetalTextureViewDepth>) {

    }
}
