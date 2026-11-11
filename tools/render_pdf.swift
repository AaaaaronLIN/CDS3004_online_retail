import Foundation
import PDFKit
import AppKit

let path = CommandLine.arguments[1]
let outDir = CommandLine.arguments[2]
let pages = CommandLine.arguments.count > 3 ? CommandLine.arguments[3].split(separator: ",").compactMap { Int($0) } : []
guard let doc = PDFDocument(url: URL(fileURLWithPath: path)) else { exit(1) }
print("PAGES: \(doc.pageCount)")
let targets = pages.isEmpty ? Array(1...doc.pageCount) : pages
for p in targets {
    guard p >= 1 && p <= doc.pageCount, let page = doc.page(at: p - 1) else { continue }
    let bounds = page.bounds(for: .mediaBox)
    let scale: CGFloat = 1.6
    let w = Int(bounds.width * scale), h = Int(bounds.height * scale)
    let img = NSImage(size: NSSize(width: w, height: h))
    img.lockFocus()
    NSColor.white.setFill()
    NSRect(x: 0, y: 0, width: w, height: h).fill()
    if let ctx = NSGraphicsContext.current?.cgContext {
        ctx.scaleBy(x: scale, y: scale)
        page.draw(with: .mediaBox, to: ctx)
    }
    img.unlockFocus()
    if let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
       let png = rep.representation(using: .png, properties: [:]) {
        let out = "\(outDir)/p\(String(format: "%02d", p)).png"
        try? png.write(to: URL(fileURLWithPath: out))
    }
}
print("done")
